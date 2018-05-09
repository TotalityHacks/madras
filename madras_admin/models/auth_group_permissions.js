'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('auth_group_permissions', {
    'group_id': {
      type: DataTypes.INTEGER,
    },
    'permission_id': {
      type: DataTypes.INTEGER,
    },
  }, {
    tableName: 'auth_group_permissions',
    underscored: true,
    timestamps: false,
    
  });

  Model.associate = (models) => {
  };

  return Model;
};

