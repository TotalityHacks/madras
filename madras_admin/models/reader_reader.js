'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('reader_reader', {
    'organization_id': {
      type: DataTypes.INTEGER,
    },
    'user_id': {
      type: DataTypes.INTEGER,
    },
  }, {
    tableName: 'reader_reader',
    underscored: true,
    timestamps: false,
    
  });

  Model.associate = (models) => {
  };

  return Model;
};

