'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('checkin_checkinevent', {
    'time': {
      type: DataTypes.DATE,
    },
    'check_in': {
      type: DataTypes.BOOLEAN,
    },
  }, {
    tableName: 'checkin_checkinevent',
    underscored: true,
    timestamps: false,
    schema: process.env.DATABASE_SCHEMA,
  });

  Model.associate = (models) => {
    Model.belongsTo(models.checkin_checkingroup, {
      foreignKey: 'check_in_group_id',
      targetKey: 'uuid',
      as: '_check_in_group_id',
    });
    
  };

  return Model;
};

